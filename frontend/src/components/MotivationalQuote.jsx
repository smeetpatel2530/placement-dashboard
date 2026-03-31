import { useState, useEffect } from 'react'

const QUOTES = [
    { text: "The secret of getting ahead is getting started.", author: "Mark Twain" },
    { text: "Success is not final, failure is not fatal — it is the courage to continue that counts.", author: "Winston Churchill" },
    { text: "Your future is created by what you do today, not tomorrow.", author: "Robert Kiyosaki" },
    { text: "Don't watch the clock; do what it does — keep going.", author: "Sam Levenson" },
    { text: "Opportunities don't happen. You create them.", author: "Chris Grosser" },
    { text: "The harder you work for something, the greater you'll feel when you achieve it.", author: "Anonymous" },
    { text: "Dream big. Start small. Act now.", author: "Robin Sharma" },
    { text: "Push yourself, because no one else is going to do it for you.", author: "Anonymous" },
    { text: "Great things never come from comfort zones.", author: "Neil Strauss" },
    { text: "Success usually comes to those who are too busy looking for it.", author: "Henry David Thoreau" },
    { text: "Don't stop when you're tired. Stop when you're done.", author: "Marilyn Monroe" },
    { text: "Wake up with determination. Go to bed with satisfaction.", author: "Anonymous" },
    { text: "It always seems impossible until it's done.", author: "Nelson Mandela" },
    { text: "Hard work beats talent when talent doesn't work hard.", author: "Tim Notke" },
    { text: "The best way to predict the future is to create it.", author: "Peter Drucker" },
    { text: "Believe you can and you're halfway there.", author: "Theodore Roosevelt" },
    { text: "You don't have to be great to start, but you have to start to be great.", author: "Zig Ziglar" },
    { text: "Strive for progress, not perfection.", author: "Tony Robins" },
    { text: "Every expert was once a beginner.", author: "Helen Hayes" },
    { text: "Your only limit is your mind.", author: "Anonymous" },
]

export default function MotivationalQuote() {
    const [index, setIndex] = useState(() => Math.floor(Math.random() * QUOTES.length))
    const [visible, setVisible] = useState(true)

    useEffect(() => {
        const interval = setInterval(() => {
            setVisible(false)
            setTimeout(() => {
                setIndex(prev => (prev + 1) % QUOTES.length)
                setVisible(true)
            }, 500)
        }, 7000)
        return () => clearInterval(interval)
    }, [])

    const quote = QUOTES[index]

    return (
        <div style={{
            marginTop: '40px',
            padding: '20px 24px',
            backgroundColor: 'rgba(255,255,255,0.02)',
            borderRadius: '12px',
            border: '1px solid rgba(255,255,255,0.06)',
            textAlign: 'center',
            transition: 'opacity 0.5s ease',
            opacity: visible ? 1 : 0,
        }}>
            <p style={{
                color: '#94a3b8',
                fontSize: '14px',
                fontStyle: 'italic',
                lineHeight: '1.6',
                marginBottom: '8px',
            }}>
                "{quote.text}"
            </p>
            <p style={{
                color: '#475569',
                fontSize: '12px',
                fontWeight: 600,
                letterSpacing: '0.03em',
            }}>
                — {quote.author}
            </p>
        </div>
    )
}