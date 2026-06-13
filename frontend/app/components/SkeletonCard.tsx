import React from 'react';

export default function SkeletonCard() {
    return (
        <div className="bg-zinc-900/70 p-5 rounded-xl border border-zinc-800 flex flex-col justify-between h-[380px] relative animate-pulse">
            {/* Top Right Buttons Placeholder */}
            <div className="absolute top-4 right-4 flex items-center gap-1">
                <div className="w-8 h-8 bg-zinc-800 rounded-full" />
                <div className="w-8 h-8 bg-zinc-800 rounded-full" />
            </div>

            <div>
                {/* Title Placeholder */}
                <div className="mb-3 pr-24">
                    <div className="h-6 bg-zinc-800 rounded-md w-3/4 mb-2" />
                    <div className="h-6 bg-zinc-800 rounded-md w-1/2" />
                </div>

                {/* Brand Placeholder */}
                <div className="h-4 bg-zinc-800/60 rounded-md w-1/3 mb-4" />

                {/* Accords Placeholder */}
                <div className="flex flex-wrap gap-2 mb-4">
                    <div className="h-5 bg-zinc-800 rounded-full w-16" />
                    <div className="h-5 bg-zinc-800 rounded-full w-20" />
                    <div className="h-5 bg-zinc-800 rounded-full w-14" />
                </div>

                {/* Meta Info Placeholder */}
                <div className="space-y-2 mt-2">
                    <div className="h-3 bg-zinc-800/60 rounded-md w-1/2" />
                    <div className="h-3 bg-zinc-800/60 rounded-md w-2/5" />
                </div>
            </div>

            {/* AI Description Button Placeholder */}
            <div className="mt-auto pt-4">
                <div className="h-10 bg-zinc-800/60 rounded-lg w-full" />
            </div>

            {/* Bottom Footer Placeholder */}
            <div className="mt-4 pt-4 border-t border-zinc-800 flex justify-between items-center">
                <div className="h-6 bg-zinc-800 rounded-full w-24" />
                <div className="h-3 bg-zinc-800/60 rounded-md w-16" />
            </div>
        </div>
    );
}