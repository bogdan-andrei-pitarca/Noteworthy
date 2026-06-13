"use client";

import Link from 'next/link';
import { useAuth } from '../context/AuthContext';
import { Droplets, Heart, LogOut, UserCircle, Hexagon } from 'lucide-react';
import { useState } from 'react';
import AuthModal from './AuthModal';


export default function Navbar() {
    const { isAuthenticated, logout } = useAuth();

    const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

    return (
        <>
            <nav className="bg-[#0a0a0f]/90 backdrop-blur-md border-b border-white/5 sticky top-0 z-50">
                <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
                    {/* Left side - Logo */}
                    <Link href="/" className="flex items-center gap-2 group">
                        <Droplets className="w-5 h-5 text-fuchsia-500 group-hover:text-fuchsia-400 transition-colors" />
                        <span className="text-2xl font-bold text-zinc-100 tracking-tight">
                            Noteworthy.
                        </span>
                    </Link>

                    {/* Navigation Links & Auth*/}
                    <div className="flex items-center space-x-6">
                        {isAuthenticated ? (
                            <>
                                <Link
                                    href="/profile"
                                    className="flex items-center text-zinc-400 hover:text-fuchsia-400 transition font-medium text-sm pr-4 md:pr-6 border-r border-zinc-800"
                                >
                                    <Hexagon className="w-4 h-4 mr-1.5" /> Scent DNA
                                </Link>
                                <Link
                                    href="/favorites"
                                    className="flex items-center text-zinc-400 hover:text-fuchsia-400 transition font-medium text-sm"
                                >
                                    <Heart className="w-4 h-4 mr-1.5" /> Favorites
                                </Link>
                                <button
                                    onClick={logout}
                                    className="flex items-center text-zinc-500 hover:text-red-400 transition font-medium text-sm pl-4 border-l border-zinc-800"
                                >
                                    <LogOut className="w-4 h-4 mr-1.5" /> Logout
                                </button>
                            </>
                        ) : (
                            <button
                                onClick={() => setIsAuthModalOpen(true)}
                                className="flex items-center bg-white/10 hover:bg-white/20 text-white px-5 py-2 rounded-full text-sm font-semibold transition-all border border-white/10"
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