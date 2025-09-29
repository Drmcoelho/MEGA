export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white mt-8">
      <div className="container mx-auto p-4 text-center">
        <p>&copy; {new Date().getFullYear()} MEGA. Todos os direitos reservados.</p>
      </div>
    </footer>
  );
}
