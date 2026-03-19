export interface Playlist {
  id: string;
  name: string;
}

export interface Track {
  item: {
    name: string;
    artists: { name: string }[];
  };
}
