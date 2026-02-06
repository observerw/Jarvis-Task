export const SyncRemindersPlugin = async ({ $, client }) => {
  return {
    event: async ({ event }) => {
      // Log event for debugging
      if (event.type === "file.watcher.updated") {
        await client.app.log({
          body: {
            service: "sync-reminders-plugin",
            level: "info",
            message: `File updated: ${event.path}`,
          },
        })
        
        if (event.path.endsWith("data/tasks.json")) {
          await client.app.log({
            body: {
              service: "sync-reminders-plugin",
              level: "info",
              message: "Tasks file changed, triggering sync...",
            },
          })
          await $`just sync-reminders`
        }
      }
    },
  }
}
