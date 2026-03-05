interface IdeaInputProps {
  onSubmit: (idea: string) => void;
  disabled: boolean;
}

export default function IdeaInput({ onSubmit, disabled }: IdeaInputProps) {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const idea = formData.get('idea') as string;
    if (idea.trim()) {
      onSubmit(idea.trim());
      e.currentTarget.reset();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <textarea
        name="idea"
        rows={4}
        placeholder="Describe your business idea in plain English..."
        disabled={disabled}
        className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 resize-y focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
        required
      />
      <button
        type="submit"
        disabled={disabled}
        className="mt-4 w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors disabled:cursor-not-allowed"
      >
        {disabled ? 'Launching...' : 'Launch VentureOS'}
      </button>
    </form>
  );
}
