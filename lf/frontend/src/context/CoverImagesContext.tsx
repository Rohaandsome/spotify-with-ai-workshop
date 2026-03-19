import React from "react";
import CoverImage from "../model/CoverImage";

const CoverImagesContext = React.createContext<{
    coverImageList: CoverImage[];
    setCoverImages: (coverImages: CoverImage[]) => void;
}>({
    coverImageList: [],
    setCoverImages: () => {},
});

export default CoverImagesContext;