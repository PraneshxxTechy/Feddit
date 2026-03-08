import { useEffect, useState } from "react";
import api from "../api/api";
import { MessageSquare, ArrowBigUp, ArrowBigDown, Share2 } from "lucide-react";

export default function Feed() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const res = await api.get("/posts");
      setPosts(res.data);
    } catch (err) {
      console.error("Failed to fetch posts:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="feed-container">Loading posts...</div>;

  return (
    <div className="feed-container">
      {posts.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
          No posts found. Be the first to post!
        </div>
      ) : (
        posts.map(post => (
          <div key={post.id} className="post-card">
            <div className="vote-sidebar">
              <ArrowBigUp size={24} className="vote-icon" />
              <span style={{ fontSize: '12px', fontWeight: 'bold' }}>{post.votes || 0}</span>
              <ArrowBigDown size={24} className="vote-icon" />
            </div>

            <div className="post-content">
              <div className="post-info">
                Posted by u/{post.username} • {post.url ? <a href={post.url} target="_blank" rel="noreferrer" style={{ color: 'var(--primary)', textDecoration: 'underline' }}>{new URL(post.url).hostname}</a> : 'self'}
              </div>
              <h3 className="post-title">{post.title}</h3>
              <p className="post-body">{post.content}</p>

              <div className="post-actions">
                <div className="action-item">
                  <MessageSquare size={16} />
                  <span>{post.comments || 0} Comments</span>
                </div>
                <div className="action-item">
                  <Share2 size={16} />
                  <span>Share</span>
                </div>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}