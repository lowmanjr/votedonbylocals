async function main(): Promise<void> {
  throw new Error(
    'Phase 2 not yet implemented — render-reel runs after card composition is approved.',
  );
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
