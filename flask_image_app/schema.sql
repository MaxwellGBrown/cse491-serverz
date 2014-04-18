drop table if exists flask_images;
create table flask_images (
  id integer primary key autoincrement,
  title text,
  image BLOB
);