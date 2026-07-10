import React from "react";

export function useTime(speed = 1) {
  const [time, setTime] = React.useState(0);
  React.useEffect(() => {
    let frame;
    const start = performance.now();
    const tick = (now) => {
      setTime(((now - start) / 1000) * speed);
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [speed]);
  return time;
}

export function Stage({ children, className = "" }) {
  return <div className={`huashu-stage ${className}`}>{children}</div>;
}

export function Sprite({ children, delay = 0, y = 24, className = "" }) {
  return (
    <div
      className={`huashu-sprite ${className}`}
      style={{
        animation: `huashu-rise 720ms cubic-bezier(.2,.8,.2,1) ${delay}ms both`,
        "--huashu-y": `${y}px`,
      }}
    >
      {children}
    </div>
  );
}

export const animationCss = `
@keyframes huashu-rise {
  from { opacity: 0; transform: translateY(var(--huashu-y)); filter: blur(8px); }
  to { opacity: 1; transform: translateY(0); filter: blur(0); }
}
.huashu-stage { width: 100%; height: 100%; }
`;
