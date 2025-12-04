"use client";

import { Counter } from "@/components/Counter";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";

export default function Home() {
  const [text, setText] = useState("");

  const handleSubmit = () => {
    console.log("Submitted text:", text);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8">
      <h1 className="text-3xl font-bold mb-8">Home Page</h1>

      <Tabs defaultValue="counter" className="w-full max-w-md">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="counter">Counter</TabsTrigger>
          <TabsTrigger value="editor">Editor</TabsTrigger>
        </TabsList>

        <TabsContent value="counter" className="mt-6">
          <div className="flex justify-center">
            <Counter />
          </div>
        </TabsContent>

        <TabsContent value="editor" className="mt-6">
          <div className="flex flex-col gap-4">
            <Textarea
              placeholder="Enter your text here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="min-h-[200px] resize-none"
            />
            <Button onClick={handleSubmit} className="w-full">
              Submit
            </Button>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
