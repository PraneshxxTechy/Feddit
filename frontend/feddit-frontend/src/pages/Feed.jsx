import { useEffect, useState } from "react";
import api from "../api/api";
import { MessageSquare, ArrowBigUp, ArrowBigDown, Share2 } from "lucide-react";
import Comments from "../components/Comments";

export default function Feed() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedComments, setExpandedComments] = useState({});

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

  const handleVote = async (e, postId, voteType) => {
    e.stopPropagation();
    try {
      await api.post(`/posts/${postId}/vote`, { vote_type: voteType });
      fetchPosts();
    } catch (err) {
      console.error("Vote error:", err);
      alert(err.response?.data?.detail || "Failed to vote. Are you logged in?");
    }
  };

  const toggleComments = (e, postId) => {
    e.stopPropagation();
    setExpandedComments(prev => ({
      ...prev,
      [postId]: !prev[postId]
    }));
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
          <div key={post.id} className="post-card-wrapper" style={{ marginBottom: '12px' }}>
            <div className="post-card" onClick={(e) => toggleComments(e, post.id)}>
              <div className="vote-sidebar">
                <ArrowBigUp
                  size={24}
                  className="vote-icon upvote"
                  onClick={(e) => handleVote(e, post.id, 1)}
                />
                <span className="vote-count">{post.votes ?? 0}</span>
                <ArrowBigDown
                  size={24}
                  className="vote-icon downvote"
                  onClick={(e) => handleVote(e, post.id, -1)}
                />
              </div>

              <div className="post-content">
                <div className="post-info">
                  Posted by u/{post.username} • {post.url ? <a href={post.url} target="_blank" rel="noreferrer" onClick={(e) => e.stopPropagation()} style={{ color: 'var(--primary)', textDecoration: 'underline' }}>{new URL(post.url).hostname}</a> : 'self'}
                </div>
                <h3 className="post-title">{post.title}</h3>
                <p className="post-body">{post.content}</p>

                <div className="post-actions">
                  <div className="action-item" onClick={(e) => toggleComments(e, post.id)}>
                    <MessageSquare size={16} />
                    <span className="count-text">{post.comments ?? 0} Comments</span>
                  </div>
                  <div className="action-item" onClick={(e) => e.stopPropagation()}>
                    <Share2 size={16} />
                    <span>Share</span>
                  </div>
                </div>
              </div>
            </div>
            {expandedComments[post.id] && (
              <div className="expanded-comments">
                <Comments postId={post.id} />
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );
}
