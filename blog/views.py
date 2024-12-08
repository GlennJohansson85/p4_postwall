from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from accounts.models import Profile
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages

from .forms import PostForm, CommentForm
from .models import Post, Comment


def postwall(request):
    posts_with_comments = []
    posts = Post.objects.filter(is_published=True).order_by('-created_at')

    for post in posts:
        comments = post.comments.all()
        posts_with_comments.append({
            'post': post,
            'comments': comments,
            'localized_created_at': localtime(post.created_at),
        })

    context = {
        'posts_with_comments': posts_with_comments,
        'user': request.user,
    }

    return render(request, "postwall.html", context)


@login_required
def post(request, post_id=None):
    """
    Handles creating and updating posts.

    If `post_id` is provided, the view attempts to update the specified post.
    Otherwise, it creates a new post. Only the post author or an admin can
    update a post. The logic ensures compatibility with local and deployed (e.g., S3) environments.
    """

    # If `post_id` is provided, retrieve the post for updating
    if post_id:
        post = get_object_or_404(Post, id=post_id)

        # Ensure only the post author or an admin can update the post
        if request.user != post.user and not request.user.is_staff:
            return HttpResponseForbidden("You are not authorized to update this post.")
    else:
        # Otherwise, initialize a new post
        post = None

    if request.method == 'POST':
        # If updating, pre-fill the form with the existing instance
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.user = request.user  # Ensure the post is linked to the user
            updated_post.save()
            messages.success(request, "Post saved successfully.")
            return redirect('postwall')
        else:
            messages.error(request, "There was an error saving your post.")
    else:
        # Initialize the form for creating or editing
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,  # Pass the post instance for context
    }

    return render(request, 'post.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            profile = get_object_or_404(Profile, user=request.user)
            comment_form.save(user=profile, post=post)
            return redirect('postwall')

    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user': request.user,
    }

    return render(request, 'post_detail.html', context)


@login_required
def add_comment(request, post_id):
    """
    Allows signed-in users to submit comments to the posts.

    Signed-in users can submit comments directly from the postwall without needing
    to go to the post details. A success message is displayed when a comment is
    successfully submitted, and the user is redirected back to post where the comment
    was made (scroll_to_post.js) in postwall.html.
    Only signed in users can add comments.
    """

    # Retrieve the post by ID or return a 404 error if not found
    post = get_object_or_404(Post, id=post_id)

    # Check if the request method is POST, indicating a comment submission
    if request.method == 'POST':
        # Get the comment text from the request
        comment_text = request.POST.get('comment_text')

        # If the comment text is not empty, create a new comment
        if comment_text:
            Comment.objects.create(
                # Link the comment to the post
                post = post,
                # Set the user as the comment author
                user = request.user,
                # Set the comment text
                text = comment_text
            )
            # Add a success message
            messages.success(request, 'Comment added successfully!')
            # Redirect the user back to the postwall page, preserving the post ID
            return redirect(f"{reverse('postwall')}?post_id={post.id}")
        else:

            # Add an error message if the comment is empty
            messages.error(request, 'Comment cannot be empty.')

    # Redirect to the postwall if the request is not POST
    return redirect('postwall')


@login_required
def delete_post_confirmation(request, post_id):
    """
    Handles the confirmation and deletion of a post.

    Retrieves a post by its `post_id` and displays a confirmation pop up to the user.
    If the user confirms the deletion (via a POST request), the post is deleted,
    and the user is redirected to the 'postwall' page. Only signed-in users/admin
    can delete posts.
    """

    # Retrieve the post by its ID, or return a 404 error if not found
    post = get_object_or_404(Post, id=post_id)

    # Check if the request method is POST (indicating the user has confirmed the deletion)
    if request.method == "POST":
        # Delete the post from the database
        post.delete()
        # Redirect the user to the 'postwall' page after deletion
        return redirect('postwall')

    # If the request method is not POST (i.e., GET), render the confirmation pop up
    context = {'post': post}
    return render(request, 'delete_post_confirmation.html', context)


@login_required
def delete_post(request, post_id):
    """
    Handles the deletion of a post.

    Retrieves a post by its `post_id` and checks if the current user is either the post's author
    or an admin. If the user is authorized, the post is deleted after confirmation, and a success message is displayed.
    Unauthorized users receive a forbidden response.
    """

    # Retrieve the post by its ID, or return a 404 error if not found
    post = get_object_or_404(Post, id=post_id)

    # Check if the logged-in user is the post's author or an admin
    if request.user == post.user or request.user.is_admin:
        # Delete the post from the database
        post.delete()
        # Display a success message to the user
        messages.success(request, 'The post has been successfully deleted.')
        # Redirect the user to the 'postwall' page after deletion
        return redirect('postwall')
    else:
        # Return a forbidden response if the user is not authorized
        return HttpResponseForbidden("You are not authorized to delete this post.")


@login_required
def delete_comment(request, comment_id):
    """
    Handles the deletion of a comment.

    Retrieves a comment by its `comment_id` and checks if the current user is either the comment's author
    or an admin. If the user is authorized, the comment is deleted, and a success message is displayed.
    Unauthorized users receive a forbidden response.
    """

    # Retrieve the comment by its ID, or return a 404 error if not found
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the logged-in user is the comment's author or an admin
    if request.user == comment.user or request.user.is_admin:
        # Delete the comment from the database
        comment.delete()
        # Display a success message to the user
        messages.success(request, 'The comment has been successfully deleted.')
        # Redirect the user to the post detail page that the comment belongs to
        return redirect('post_detail', post_id=comment.post.id)

    else:
        # Return a forbidden response if the user is not authorized
        return HttpResponseForbidden("You are not authorized to delete this comment.")


def search(request):
    """
    Handles the search functionality for posts.

    This view retrieves posts from the database that match the given keyword
    in their titles. If a keyword is provided in the GET request, it filters
    the posts accordingly. The results are then rendered in the
    'search_results.html' template.
    """

    # Retrieve the search keyword from the GET parameters, defaulting to an empty string if not provided
    keyword = request.GET.get('keyword', '')
    # Initialize an empty list to hold the matching posts
    posts = []

    # If a keyword is provided, filter posts that contain the keyword in their titles
    if keyword:
        posts = Post.objects.filter(title__icontains=keyword)

    # Render the 'search_results.html' template with the list of matching posts
    return render(request, 'search_results.html', {'posts': posts})


def search_suggestions(request):
    """
    Provides search suggestions based on the keyword.

    This view responds to AJAX requests by returning a JSON object containing
    suggested post titles that match the given keyword. The suggestions are
    limited to a maximum of 10 results.
    """

    # Retrieve the search keyword from the GET parameters, defaulting to an empty string if not provided
    keyword = request.GET.get('keyword', '')

    # Initialize an empty list to hold the suggested Post titles
    suggestions = []

    # If a keyword is provided, filter posts that contain the keyword in their titles
    if keyword:
        # Limit results to 10
        posts = Post.objects.filter(title__icontains=keyword)[:10]
        # Create a list of dictionaries with post id and title for each matching post
        suggestions = [{'id': post.id, 'title': post.title} for post in posts]

    # Return the suggestions as a JSON response
    return JsonResponse({'suggestions': suggestions})
