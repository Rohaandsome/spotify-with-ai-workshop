// Check if user ID exists in localStorage
import { v4 } from "uuid";

export function useUserId() {
  let userId = localStorage.getItem("user_id");

  if (!userId) {
    userId = v4();
    localStorage.setItem("user_id", userId);
  }
  return userId;
}
