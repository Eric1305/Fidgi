"use client";

import { useAuth, useUser } from "@clerk/nextjs";
import { useEffect, useState } from "react";

interface UserProfile {
  id: number;
  clerk_user_id: string;
  name: string;
  email: string;
  created_at: string;
}

export default function TestProfile() {
  const { getToken } = useAuth();
  const { user } = useUser();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [allUsers, setAllUsers] = useState<UserProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(() => {
    async function fetchData() {
      try {
        const token = await getToken();

        // Fetch current user profile
        const profileResponse = await fetch(`${API_URL}/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (!profileResponse.ok) {
          throw new Error(`Failed to fetch profile: ${profileResponse.status}`);
        }

        const profileData = await profileResponse.json();
        setProfile(profileData);

        // Fetch all users
        const usersResponse = await fetch(`${API_URL}/users`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (!usersResponse.ok) {
          throw new Error(`Failed to fetch users: ${usersResponse.status}`);
        }

        const usersData = await usersResponse.json();
        setAllUsers(usersData);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    }

    if (user) {
      fetchData();
    }
  }, [user, getToken, API_URL]);

  const mono = { fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace' } as const;

  if (loading) {
    return <div style={{ padding: '1rem', color: 'white', ...mono }}>Loading…</div>;
  }

  if (error) {
    return (
      <div style={{ padding: '1rem', color: 'white', ...mono }}>
        ERROR: {error}\nBackend: {API_URL}
      </div>
    );
  }

  return (
    <pre style={{ padding: '1rem', margin: 0, color: 'white', background: 'transparent', ...mono }}>
Test Page
--------------------------------------------------
Clerk User:
  ID: {user?.id}
  Name: {user?.fullName}
  Email: {user?.primaryEmailAddress?.emailAddress}

Database Profile (/me):
{profile ? `  DB ID: ${profile.id}
  Clerk User ID: ${profile.clerk_user_id}
  Name: ${profile.name || 'N/A'}
  Email: ${profile.email || 'N/A'}
  Created At: ${new Date(profile.created_at).toLocaleString()}` : '  <none>'}

All Users (/users): count={allUsers.length}
{allUsers.map(u => `  - id=${u.id} clerk_user_id=${u.clerk_user_id} name=${u.name || 'N/A'} email=${u.email || 'N/A'} created=${new Date(u.created_at).toLocaleDateString()}`).join('\n') || '  <none>'}

Checks:
  Auth token passed: {Boolean(user) ? 'yes' : 'no'}
  Profile loaded: {profile ? 'yes' : 'no'}
  Users loaded: {allUsers.length > 0 ? 'yes' : 'no'}
  Backend URL: {API_URL}
--------------------------------------------------
    </pre>
  );
}