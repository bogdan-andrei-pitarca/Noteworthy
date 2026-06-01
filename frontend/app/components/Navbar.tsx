"use client";

import Link from 'next/link';
import { useAuth } from '../context/AuthContext';
import { Heart, LogOut, UserCircle } from 'lucide-react';
import { useState } from 'react';
import AuthModal from './AuthModal';


export default function Navbar() {
    const { isAuthenticated, logout } = useAuth();

    const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

    return (
        <>
            <nav className="bg-white border-b border-gray-100 shadow-sm sticky top-0 z-50">
                <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
                    {/* Left side - Logo */}
                    <Link href="/" className="text-2xl font-extrabold text-fuchsia-800 tracking-tight">
                        Noteworthy.
                    </Link>

                    {/* Navigation Links & Auth*/}
                    <div className="flex items-center space-x-6">
                        {isAuthenticated ? (
                            <>
                                <Link
                                    href="/favorites"
                                    className="flex items-center text-gray-600 hover:text-fuchsia-600 transition font-medium text-sm"
                                >
                                    <Heart className="w-4 h-4 mr-1.5" /> Favorites
                                </Link>
                                <button
                                    onClick={logout}
                                    className="flex items-center text-gray-500 hover:text-red-600 transition font-medium text-sm pl-4 border-l border-gray-200"
                                >
                                    <LogOut className="w-4 h-4 mr-1.5" /> Logout
                                </button>
                            </>
                        ) : (
                            <button
                                onClick={() => setIsAuthModalOpen(true)}
                                className="flex items-center bg-fuchsia-600 text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-fuchsia-700 transition shadow-sm"
                            >
                                <UserCircle className="w-4 h-4 mr-2" /> Sign In
                            </button>
                        )}
                    </div>
                </div>
            </nav>

            <AuthModal isOpen={isAuthModalOpen} onClose={() => setIsAuthModalOpen(false)} />
        </>
    );
}