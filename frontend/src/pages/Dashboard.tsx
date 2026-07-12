import { useQuery } from "@tanstack/react-query";
import StatsCard from "../components/StatsCard";
import { getDashboardStats } from "../api/dashboard";

export default function Dashboard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["dashboard"],
    queryFn: getDashboardStats,
  });

  if (isLoading) return <h1>Loading...</h1>;

  if (error) return <h1>Failed to load dashboard.</h1>;

  return (
    <div>
      <h1 className="text-4xl font-bold mb-8">Dashboard</h1>

      <div className="grid grid-cols-4 gap-6">
        <StatsCard title="Jobs" value={data?.jobs ?? 0} />

        <StatsCard title="Workers" value={data?.workers ?? 0} />

        <StatsCard title="Projects" value={data?.projects ?? 0} />

        <StatsCard title="Queues" value={data?.queues ?? 0} />
      </div>
    </div>
  );
}
