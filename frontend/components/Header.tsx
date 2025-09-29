import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto p-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-blue-600">
          MEGA
        </Link>
        <nav>
          <ul className="flex space-x-4">
            <li><Link href="/modules" className="text-gray-600 hover:text-blue-600">Módulos</Link></li>
            <li><Link href="/about" className="text-gray-600 hover:text-blue-600">Sobre</Link></li>
            <li><Link href="/login" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Login</Link></li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
