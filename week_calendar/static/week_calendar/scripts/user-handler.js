export async function getUserID() {
    try {
        const response = await fetch("/current-user/");
        if (!response.ok) throw new Error("Failed to fetch user data");

        const data = await response.json();
        return data.user_id;
    } catch (error) {
        console.error("Error fetching user ID:", error);
        return null;
    }
}