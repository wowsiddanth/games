"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useEffect, useRef, useState } from "react";

export default function Home() {
	const chipType = useRef<number>(0);

	const [slots, setSlots] = useState<string[]>([]);

	const handleButtonOnClick = () => {
		fetch('http://localhost:5000/reset')
			.then(res => {
				if (res.ok) {
					// Some re-render logic here.
				}
			})
	}

	const handleOnClick = (position: number) => {
		const stringChipType: string = chipType.current == 0 ? 'blue' : 'red';
		const stringChipType2: string = chipType.current == 0 ? 'B' : 'R';

		const updatedSlots = [...slots];
		let smallestIndex = position;

		if (slots[position] != '#') {
			return;
		}

		for (let i = smallestIndex; i <= 41; i += 7) {
			if (slots[i] != '#') {
				break
			} else {
				smallestIndex = i;
			}
		}

		updatedSlots[smallestIndex] = stringChipType2;
		setSlots(updatedSlots);

		fetch('http://localhost:5000/place', {
			headers: {
				'Content-Type': 'application/json',
			},
			method: "POST",
			body: JSON.stringify({
				'column': position % 7,
				'chip_type': stringChipType,
			})
		}).then(res => res.json()).then(data => {
			if (data.current_state.toString() != updatedSlots.toString()) {
				console.log("do jAnot match!!!!!!!!!!!!!!!")
			} else {
			}
		});

		chipType.current = 1 - chipType.current;
	}

	useEffect(() => {
		fetch('http://localhost:5000/')
			.then(res => res.json())
			.then(data => setSlots(data))
	}, []);

	return (
		<div className="items-center justify-items-center min-h-screen p-8 pb-20 bg-black gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
			<main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
				<div className="flex gap-10">
					<div className="flex flex-col gap-4">
						<div className="text-white text-4xl text-start font-bold">Connect Four</div>
						<div className="text-white text-md text-start max-w-96">Click on any cell to place a chip in that column.</div>
					</div>
					<div className="flex flex-col gap-2">
						<Button onClick={() => handleButtonOnClick()}>Reset</Button>
						<div className="grid grid-cols-7 gap-2">
							{
								slots && slots.map((slot, i) => <div className="hover:bg-zinc-800 h-20 w-20 gap-4 rounded-md hover:scale-110 bg-zinc-900 transition-all border-4 border-transparent hover:border-violet-400" key={i}>
									<div className={cn("w-full h-full flex justify-center items-center text-6xl font-semibold font-mono", slot == 'B' && 'text-blue-400', slot == 'R' && 'text-red-600', (slot != 'B' && slot != 'R') && 'text-neutral-800')} onClick={() => handleOnClick(i)}>{slot == 'R' && slot || slot == 'B' && slot}</div>
								</div>)
							}
						</div>
					</div>
				</div>
			</main>
		</div>
	);
}
