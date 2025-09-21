import { useState } from 'react';
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";

interface InputFormProps {
  onGenerate: (data: { topic: string; description: string }) => void;
  isLoading: boolean;
}

export function InputForm({ onGenerate, isLoading }: InputFormProps) {
  const [topic, setTopic] = useState<string>('');
  const [description, setDescription] = useState<string>('');

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    onGenerate({ topic, description }); 
  };

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Create Your TopicBook</CardTitle>
        <CardDescription>
          Enter a topic and provide a description of your learning goals and background.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <fieldset disabled={isLoading} className="grid w-full items-center gap-6">
            <div className="flex flex-col space-y-2">
              <Label htmlFor="topic">Topic</Label>
              <Input 
                id="topic" 
                placeholder="e.g., Introduction to Quantum Computing" 
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                required
              />
            </div>
            <div className="flex flex-col space-y-2">
              <Label htmlFor="description">Description (Optional)</Label>
              <Textarea 
                id="description" 
                placeholder="Describe your needs... e.g., 'I am a biologist...'"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>
            <Button type="submit" className="w-full">
              {isLoading ? 'Generating...' : 'Generate TopicBook'}
            </Button>
          </fieldset>
        </form>
      </CardContent>
    </Card>
  );
}