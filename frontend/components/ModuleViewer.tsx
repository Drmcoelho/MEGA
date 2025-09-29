type ModuleViewerProps = {
  moduleName: string;
  content: string; // Conteúdo em Markdown
  quizJson: string; // Quiz em formato JSON
};

export default function ModuleViewer({ moduleName, content, quizJson }: ModuleViewerProps) {
  // Por enquanto, este componente apenas exibe o nome do módulo.
  // No futuro, ele irá renderizar o Markdown e o quiz interativo.
  return (
    <div>
      <h2 className="text-3xl font-bold mb-4">Módulo: {moduleName}</h2>
      
      <div className="prose lg:prose-xl max-w-none">
        <h3 className="text-2xl font-semibold">Conteúdo</h3>
        {/* Aqui entrará a renderização do Markdown */}
        <p>{content}</p>
      </div>

      <div className="mt-8">
        <h3 className="text-2xl font-semibold">Quiz</h3>
        {/* Aqui entrará a renderização do quiz interativo */}
        <pre className="bg-gray-100 p-4 rounded mt-2">{quizJson}</pre>
      </div>
    </div>
  );
}
