import axios from "axios";

const api_posts = axios.create({
  baseURL: "http://127.0.0.1:5000",
  withCredentials: false,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

export default {
  getPosts() {
    return api_posts.get("/posts");
  },
  postPost(post) {
    return api_posts.post("/posts", post);
  },
  deletePost(id_post) {
    return api_posts.delete("/posts/" + id_post);
  },
};
