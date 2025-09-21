import { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface Book {
  filename: string;
  content: string;
}

export function BookViewer() {
  const [books, setBooks] = useState<string[]>([]);
  const [selectedBook, setSelectedBook] = useState<Book | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  useEffect(() => {
    axios.get('http://localhost:8000/books')
      .then(response => setBooks(response.data))
      .catch(error => console.error("Error fetching book list:", error));
  }, []);

  const handleBookClick = async (filename: string) => {
    try {
      const response = await axios.get(`http://localhost:8000/books/${filename}`);
      setSelectedBook(response.data);
      setIsDialogOpen(true);
    } catch (error) {
      console.error("Error fetching book content:", error);
    }
  };

  return (
    <>
      <div className="h-full p-4 flex flex-col">
        <h2 className="text-xl font-semibold mb-4 text-center">Generated Books</h2>
        <div className="flex-grow overflow-y-auto">
          {books.length > 0 ? (
            <div className="flex flex-col gap-2">
              {books.map((bookFile) => (
                <Button
                  key={bookFile}
                  variant="ghost"
                  className="justify-start text-left"
                  onClick={() => handleBookClick(bookFile)}
                >
                  {bookFile.replace(".md", "").replace(/_/g, " ")}
                </Button>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground text-center">No books generated yet.</p>
          )}
        </div>
      </div>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-4xl h-[90vh] flex flex-col">
          <DialogHeader>
            <DialogTitle>{selectedBook?.filename.replace(".md", "").replace(/_/g, " ")}</DialogTitle>
          </DialogHeader>
          <div className="flex-grow overflow-y-auto pr-6 prose prose-invert">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {selectedBook?.content || "Loading..."}
            </ReactMarkdown>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}