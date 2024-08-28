export function formatTime(time: number): string {
  const hours = Math.floor(time / 3600);
  const minutes = Math.floor((time % 3600) / 60);
  const seconds = Math.floor(time % 60);

  if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  } else if (minutes > 0) {
      return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  } else {
      return `0:${seconds.toString().padStart(2, '0')}`;
  }
}
