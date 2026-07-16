'use client';

import { useState, useRef, useEffect } from 'react';
import { chat, uploadFiles } from '@/lib/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [uploadedCount, setUploadedCount] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setUploading(true);
    setUploadStatus('⏳ 上传中...');

    try {
      const result = await uploadFiles(files);
      const count = result.files?.length || 0;
      const newTotal = uploadedCount + count;
      setUploadedCount(newTotal);
      
      setUploadStatus(`✅ 成功上传 ${count} 个文件（共 ${newTotal} 个文件已入库）`);

      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }

      // 移除旧的系统消息（以 "📄" 开头的消息），保留最新的汇总
      const filteredMessages = messages.filter(msg => !msg.content.startsWith('📄'));
      setMessages([
        ...filteredMessages,
        {
          role: 'assistant',
          content: `📄 已上传 ${newTotal} 个文件，知识库已更新！`
        }
      ]);
    } catch (error) {
      setUploadStatus('❌ 上传失败，请检查后端服务');
      console.error('上传失败:', error);
    } finally {
      setUploading(false);
      setTimeout(() => setUploadStatus(''), 4000);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const result = await chat(userMessage);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: result.answer || '未获取到回答' 
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: '❌ 请求失败，请检查后端是否启动' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* 头部 */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-800">📚 AI知识库智能问答</h1>
          <p className="text-sm text-gray-500">基于私有知识库的智能问答系统</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              uploading 
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                : 'bg-green-500 text-white hover:bg-green-600'
            }`}
          >
            {uploading ? '⏳ 上传中...' : '📤 上传文档'}
          </button>
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".txt,.pdf,.docx"
            onChange={handleFileUpload}
            className="hidden"
          />
        </div>
      </header>

      {/* 状态提示条 */}
      {uploadStatus && (
        <div className={`px-6 py-2 text-sm text-center ${
          uploadStatus.includes('✅') ? 'bg-green-50 text-green-700' : 
          uploadStatus.includes('❌') ? 'bg-red-50 text-red-700' :
          'bg-blue-50 text-blue-700'
        }`}>
          {uploadStatus}
        </div>
      )}

      {/* 消息列表 */}
      <div className="flex-1 overflow-y-auto px-4 py-6 max-w-3xl mx-auto w-full">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-gray-400">
            <div className="text-6xl mb-4">🤖</div>
            <p className="text-lg">欢迎使用 AI 知识库问答系统</p>
            <p className="text-sm">点击「上传文档」添加知识库，然后开始提问</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex mb-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-3 ${
                  msg.role === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white border border-gray-200 text-gray-800'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex justify-start mb-4">
            <div className="bg-white border border-gray-200 rounded-lg px-4 py-3 text-gray-400">
              <span className="inline-block animate-pulse">🤔 思考中...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* 输入框 */}
      <div className="border-t border-gray-200 bg-white px-4 py-4">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="请输入您的问题..."
            className="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className={`px-6 py-2.5 rounded-lg font-medium transition-colors ${
              loading || !input.trim()
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            {loading ? '发送中...' : '发送'}
          </button>
        </form>
      </div>
    </div>
  );
}