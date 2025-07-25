"use client";

import { useState, useEffect, FormEvent } from "react";

interface Post {
  text: string;
  image_url: string;
}

export default function Home() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [text, setText] = useState("");
  const [image, setImage] = useState<File | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/posts/")
      .then((response) => response.json())
      .then((data) => setPosts(data));
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!image) {
      alert("Please select an image.");
      return;
    }

    const formData = new FormData();
    formData.append("text", text);
    formData.append("image", image);

    const response = await fetch("http://localhost:8000/posts/", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const newPost = await response.json();
      setPosts([newPost, ...posts]);
      setText("");
      setImage(null);
    } else {
      alert("Failed to create post.");
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Insta-clone</h1>

      <form onSubmit={handleSubmit} className="mb-8">
        <div className="mb-4">
          <label htmlFor="text" className="block text-gray-700 font-bold mb-2">
            Post Text
          </label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            rows={3}
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="image" className="block text-gray-700 font-bold mb-2">
            Image
          </label>
          <input
            type="file"
            id="image"
            accept="image/*"
            onChange={(e) => setImage(e.target.files?.[0] || null)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
        </div>
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          Create Post
        </button>
      </form>

      <div>
        {posts.map((post, index) => (
          <div key={index} className="border rounded-lg p-4 mb-4">
            <img
              src={`http://localhost:8000${post.image_url}`}
              alt={post.text}
              className="w-full h-auto rounded-lg mb-2"
            />
            <p>{post.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
