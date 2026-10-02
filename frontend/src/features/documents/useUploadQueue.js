import { useCallback, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { docKeys, uploadDocument } from "./api";

let seq = 0;

/** Upload state machine for many files at once. Returns [items, enqueue]. */
export function useUploadQueue() {
  const qc = useQueryClient();
  const [items, setItems] = useState([]);

  const patch = useCallback((id, changes) => {
    setItems((list) => list.map((it) => (it.id === id ? { ...it, ...changes } : it)));
  }, []);

  const remove = useCallback((id) => setItems((list) => list.filter((it) => it.id !== id)), []);

  const enqueue = useCallback(
    (files) => {
      for (const file of files) {
        const id = ++seq;
        const { promise, abort } = uploadDocument(file, {
          onProgress: (p) => patch(id, { progress: p }),
        });
        setItems((list) => [...list, { id, file, progress: 0, status: "uploading", abort }]);
        promise
          .then((doc) => {
            patch(id, { status: "done", progress: 1, docId: doc.id });
            qc.invalidateQueries({ queryKey: docKeys.all });
            setTimeout(() => remove(id), 1600);
          })
          .catch((err) => {
            if (err.code === "aborted") return remove(id);
            patch(id, {
              status: "error",
              error: err.message,
              existingId: err.problem?.document_id,
            });
          });
      }
    },
    [patch, remove, qc],
  );

  return { items, enqueue, remove };
}
