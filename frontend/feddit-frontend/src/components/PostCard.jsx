import api from "../api/api";

export default function PostCard({ post, refreshPosts }) {

  const vote = async (value) => {
    await api.post(`/posts/${post.id}/vote`, {
      vote_type: value
    });

    refreshPosts();
  };

  return (
    <div style={{border:"1px solid gray", margin:"10px"}}>

      <h3>{post.title}</h3>

      <p>{post.content}</p>

      <p>Posted by {post.username}</p>

      <p>Votes: {post.votes}</p>
      <p>Comments: {post.comments}</p>

      <button onClick={()=>vote(1)}>⬆️</button>
      <button onClick={()=>vote(-1)}>⬇️</button>

    </div>
  );
}