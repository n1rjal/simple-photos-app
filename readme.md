

## Google Photos

This is a web application (not mobile responsive) designed for managing photos with various features related to users, photos, and albums.

### Requirements

- Users: Authentication, logout
- Photos: Sharing functionality
- Albums: Ability to manage photos within albums, both shared and private

### Models

**User**
- Django default user model with additional timestamps:
  - created_at
  - updated_at
  - deleted_at (soft deletion)

**Photo**
- Represents a photo with:
  - name
  - url
  - metadata
  - owner (linked to a user)

**PhotoMetaData**
- Additional metadata for a photo:
  - capture_time
  - linked to a photo

**PhotoUser**
- Many-to-many relationship between users and photos:
  - photo
  - user

**PhotoAlbum**
- Many-to-many relationship between photos and albums:
  - photo
  - album

**Album**
- Represents an album with:
  - name
  - user (owner of the album)
  - timestamps for creation and update

### API Endpoints

**Photo**

- **POST** `/photos/` - Upload a photo with scanning and metadata extraction.
- **GET** `/photos/` - Retrieve photos with pagination, sorting, and optional filtering by album.
- **DELETE** `/photos/:photo_id/` - Delete a specific photo.

**PhotoUser**

- **POST** `/photos/:photo_id/share/` - Assign a photo to users by `photo_id`.
- **POST** `/photos/:photo_id/unshare/` - Unassign a photo from users by `photo_id`.

**Album**

- **POST** `/albums/` - Create a new album.
- **GET** `/albums/` - List all albums.
- **POST** `/albums/:album_id/photos/share/` - Add photos to an album by `album_id`.
- **DELETE** `/albums/:album_id/photos/unshare/` - Remove photos from an album by `album_id`.
- **PUT** `/albums/:album_id/` - Update album details by `album_id`.
- **DELETE** `/albums/:album_id/` - Delete an album by `album_id`.
- **POST** `/albums/:album_id/user/share/` - Share an album with specified users by `album_id`.
- **POST** `/albums/:album_id/user/unshare/` - Remove access to an album from specified users by `album_id`.

**AlbumAccess**

- Many-to-many relationship between users and albums.
