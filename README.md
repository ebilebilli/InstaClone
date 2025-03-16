# Social Media API Project

A Django-based REST API for a social media platform, featuring posts, stories, profiles, direct messages, likes, and comments. The API supports both public and private interactions with robust authentication and permission controls.

---

## 🚀 Features

- **Posts**: Create, retrieve, update, and delete posts. Like posts and manage comments.
- **Stories**: Create, retrieve, and delete stories. Like stories and send messages to story owners.
- **Profiles**: Search profiles, view profile details, follow/unfollow users, and manage followers/followings.
- **Direct Messages**: Send and manage messages between users.
- **Likes**: Like posts, stories, and comments.
- **Comments**: Add, update, and delete comments on posts.

---

## 📂 Project Structure

- **`apis/`**: Main API views and URL routing.
- **`profiles/`**: User profile management (follow/unfollow, profile details).
- **`posts/`**: Post creation, retrieval, updating, and deletion.
- **`stories/`**: Story creation, retrieval, and deletion.
- **`direct_messages/`**: Direct messaging between users.
- **`likes/`**: Like management for posts, stories, and comments.
- **`comments/`**: Comment management for posts.

---

## 🔑 Authentication & Permissions

- **Token Authentication**: Users must authenticate using a token to access protected endpoints.
- **Permissions**:
  - **`IsAuthenticated`**: Ensures the user is logged in.
  - **`HeHasPermission`**: Custom permission for accessing private profiles, posts, and stories.
  - **`IsOwner`**: Ensures the user is the owner of the resource (e.g., post, story, comment).

---

## 🌐 API Endpoints

### Posts
- **`GET /open_posts/`**: Retrieve all posts from open profiles.
- **`GET /private_posts/`**: Retrieve all posts from private profiles (requires authentication).
- **`POST /post_create/`**: Create a new post.
- **`GET /private_post_detail/<int:post_id>/`**: Retrieve details of a private post.
- **`GET /open_post_detail/<int:post_id>/`**: Retrieve details of an open post.
- **`POST /open_post/<int:post_id>/like_post/`**: Like or unlike an open post.
- **`POST /private_post/<int:post_id>/like_post/`**: Like or unlike a private post.
- **`GET /post/<int:post_id>/comments/`**: Retrieve comments for a post.
- **`PATCH /post/<int:comment_id>/`**: Update a comment.
- **`POST /post/<int:comment_id>/like_comment`**: Like or unlike a comment.

### Stories
- **`GET /stories/`**: Retrieve all open stories.
- **`POST /story_create/`**: Create a new story.
- **`GET /open_story_detail/<int:story_id>/`**: Retrieve details of an open story.
- **`GET /private_story_detail/<int:story_id>/`**: Retrieve details of a private story.
- **`POST /private_story/<int:story_id>/like_story`**: Like or unlike a private story.
- **`POST /open_story/<int:story_id>/like_story`**: Like or unlike an open story.
- **`POST /open_story/<int:story_id>/send_message_to_story`**: Send a message to the owner of an open story.
- **`POST /private_story/<int:story_id>/send_message_to_story`**: Send a message to the owner of a private story.

### Profiles
- **`GET /profiles/search`**: Search profiles by username.
- **`GET /profile_detail/<int:profile_id>/`**: Retrieve profile details.
- **`POST /profile_detail/<int:profile_id>/`**: Follow a profile.
- **`DELETE /profile_detail/<int:profile_id>/`**: Unfollow a profile.
- **`GET /profile_followers/<int:profile_id>/`**: Retrieve followers of a profile.
- **`GET /profile_followings/<int:profile_id>/`**: Retrieve profiles a user is following.
- **`GET /profile_message_list/<int:profile_id>/`**: Retrieve messages for a profile.
- **`POST /send_message_to_open_profile/<int:profile_id>/`**: Send a message to an open profile.
- **`POST /send_message_to_private_profile/<int:profile_id>/`**: Send a message to a private profile.
- **`GET /manage_message_with_open_profile/<int:profile_id>/`**: Manage messages with an open profile.
- **`GET /manage_message_with_private_profile/<int:profile_id>/`**: Manage messages with a private profile.

---

## 🛠️ Setup & Installation

1. **Clone the repository**:
```bash
git clone https://github.com/ebilebilli/InstaClone
cd InstaClone

**Virtual Environment Setup**:
   - Replaced `venv` instructions with `pipenv` commands.
   - Added steps to install `pipenv` if it's not already installed.
   - Used `pipenv install` to create the virtual environment and install dependencies.
   - Used `pipenv shell` to activate the virtual environment.

Install dependencies:
pip install -r requirements.txt

Set up the database:
Run migrations to create the database schema:
python manage.py migrate
Create a superuser (optional):

Create an admin user to access the Django admin panel:
python manage.py createsuperuser

Run the development server:
python manage.py runserver

Access the API:
The API will be available at:
http://127.0.0.1:8000/
You can explore the API endpoints using tools like Postman or Swagger.