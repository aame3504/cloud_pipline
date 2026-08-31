import { useMutation } from "@tanstack/react-query";

import {
    searchImageRag,
} from "../api/imageragApi";


export const useImageRagMutation = () => {
    return useMutation({
        mutationFn: searchImageRag,
    });
};