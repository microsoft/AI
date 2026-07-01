# TF-IDF Chatbot — Incremental Learning Fix

Context: [issue #157](https://github.com/microsoft/AI/issues/157) shared a small TF-IDF
retrieval chatbot. A review comment on that issue noted that `learn_from_pair`
rebuilt the TF-IDF vectorizer from scratch on every call, making each call cost
O(n) and a full learning session cost O(n²).

This sample applies the suggested fix: `learn_from_pair` now reuses the
already-fitted vectorizer's `transform()` to encode just the new example and
appends it to the existing TF-IDF matrix with `scipy.sparse.vstack`, which is
O(1) amortized per call. A full rebuild only runs periodically (every
`rebuild_every` additions, default 20) to resync the vocabulary/IDF weights
with any new terms.

For larger-scale use, a vector database (FAISS/Chroma) would be a better
long-term choice, since it also avoids the linear `cosine_similarity` scan in
`respond()`. This sample keeps the original script's shape and targets just
the specific O(n²) issue with a minimal change.
