import { useEffect, useState } from "react";
import api from "../api/api";

export default function Comments({ postId }) {

  const [comments, setComments] = useState([]);
  const [content, setContent] = useState("");

  const fetchComments = async () => {
    const res = await api.get(`/posts/${postId}/comments`);
    setComments(res.data);
  };

  const addComment = async () => {
    await api.post(`/posts/${postId}/comments`, { content });
    setContent("");
    fetchComments();
  };

  useEffect(()=>{
    fetchComments();
  }, []);

  return (
    <div>

      <h4>Comments</h4>

      {comments.map(c => (
        <p key={c.id}>{c.content} - {c.username}</p>
      ))}

      <input
        value={content}
        onChange={(e)=>setContent(e.target.value)}
      />

      <button onClick={addComment}>Add Comment</button>

    </div>
  );
}