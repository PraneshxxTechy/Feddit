import { useEffect, useState } from "react";
import api from "../api/api";

export default function Comments({ postId }) {

  const [comments, setComments] = useState([]);
  const [comment, setComment] = useState("");

  const fetchComments = async () => {
    const res = await api.get(`/posts/${postId}/comments`);
    setComments(res.data);
  };

  const addComment = async () => {
    try {
      await api.post(`/posts/${postId}/comments`, { comment });
      setComment("");
      fetchComments();
    } catch (err) {
      console.error("Comment error:", err);
      alert(err.response?.data?.detail || "Failed to add comment. Are you logged in?");
    }
  };

  useEffect(() => {
    fetchComments();
  }, []);

  return (
    <div className="comments-section">
      <h4>Comments</h4>
      <div className="comments-list">
        {comments.map(c => (
          <div key={c.id} className="comment-item">
            <p><strong>u/{c.username}</strong>: {c.comment}</p>
          </div>
        ))}
      </div>

      <input
        className="comment-input"
        placeholder="Add a comment..."
        value={comment}
        onChange={(e) => setComment(e.target.value)}
      />

      <button className="primary-btn" onClick={addComment}>Add Comment</button>

    </div>
  );
}