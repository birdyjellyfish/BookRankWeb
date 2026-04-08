export interface Genre {
  genreid: number;
  name: string;
}

export interface Book {
  bookid: number;
  goodreadsbookid: number;
  coverid: number;
  isbn: string;
  authors: string;
  title: string;
  averagerating: number;
  weightedscore: number;
  ratingscount: number;
  genres: Array<Genre>;
}

export interface BookLite {
  bookid: number;
  coverid: number;
  authors: string;
  title: string;
}

export interface BookUser {
  bookid: number;
  coverid: number;
  authors: string;
  title: string;
  datefinished: string;
}

export interface BookSearch {
  count: number;
  next: string | null;
  previous: string | null;
  results: BookLite[];
}

export interface User {
  id: number;
  username: string;
  email: string;
}