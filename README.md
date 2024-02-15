# RAGit!
A framework to create a RAG assistant for videos.


## To Do
- [ ] Get text from video 
  - [x] Youtube API (unofficial)
  - [ ] GCP StT automatic
  - [ ] Local StT models (abstract class)
- [x] Function to perform embedding (multilingual gecko)
- [x] Lift Vector DB (vector search? or Chroma?)
- [x] RAG prompt (query answer)
- [x] Generate citations to document/chunk (Check grounding? Citation?)
- [x] Get starting time for a chunk
- [ ] Wrap up all together

### Extra mile
- [ ] Implement [Semantic Chunking](https://python.langchain.com/docs/modules/data_connection/document_transformers/semantic-chunker) to create chunks (default is len words)
- [ ] Optimize StT by adding punctuation (LLM calling)
- [ ] Dynamically select the prompt by using the language in the video (worth it?  what if query is in a != language?)
- [ ] Enable RAG fusion


## Videos
1 - [El ORIGEN de los distintos ACENTOS de Argentina](https://www.youtube.com/watch?v=NgbEL2HbXWw), id: NgbEL2HbXWw
