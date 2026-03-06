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
    <form onSubmit={handleSubmit} className="w-full max-w-[680px] mx-auto">
      <textarea
        name="idea"
        rows={4}
        placeholder="describe the idea."
        disabled={disabled}
        className="w-full px-0 py-3 bg-[#F0EDE8] border-0 border-b border-[#1a1a1a] text-[#1a1a1a] placeholder-[#888] resize-none focus:outline-none disabled:opacity-50"
        style={{ fontFamily: 'system-ui, sans-serif', fontSize: '15px' }}
        required
      />
      <button
        type="submit"
        disabled={disabled}
        className="mt-6 w-full bg-[#1a1a1a] hover:bg-[#F0EDE8] text-[#F0EDE8] hover:text-[#1a1a1a] h-12 transition-colors disabled:opacity-50 hover:outline hover:outline-1 hover:outline-[#1a1a1a]"
        style={{ 
          fontFamily: 'system-ui, sans-serif', 
          fontSize: '13px', 
          letterSpacing: '0.1em', 
          textTransform: 'uppercase',
          borderRadius: '2px'
        }}
      >
        {disabled ? 'working' : 'launch'}
      </button>
    </form>
  );
}
