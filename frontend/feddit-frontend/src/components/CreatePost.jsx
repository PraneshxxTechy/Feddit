import { useState } from "react";
import api from "../api/api";

export default function CreatePost({ refreshPosts }) {

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [url, setUrl] = useState("");

  const handleSubmit = async () => {

    await api.post("/posts", {
      title,
      content,
      url
    });

    setTitle("");
    setContent("");
    setUrl("");

    refreshPosts();
  };

  return (
    <div>
      <h3>Create Post</h3>

      <input
        placeholder="Title"
        value={title}
        onChange={(e)=>setTitle(e.target.value)}
      />

      <textarea
        placeholder="Content"
        value={content}
        onChange={(e)=>setContent(e.target.value)}
      />

      <input
        placeholder="URL"
        value={url}
        onChange={(e)=>setUrl(e.target.value)}
      />

      <button onClick={handleSubmit}>Post</button>
    </div>
  );
}