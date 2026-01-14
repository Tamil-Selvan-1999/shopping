---
name: nextjs-expert
description: Guides GitHub Copilot to use Next.js App Router, React Server Components, and Tailwind CSS best practices.
license: MIT
---

# Next.js Expert Guidance

When generating code for this project, adhere to the following principles:

## 🎯 Code Generation Priorities

- **TypeScript-first:** Always use TypeScript with `strict` mode enabled. Use explicit types for props and API responses.
- **Server-first:** Default to [React Server Components (RSC)](nextjs.org) unless client interactivity (event handlers, effects, browser APIs) is specifically required.
- **Performance-first:** Optimize for Core Web Vitals. Minimize client-side JavaScript.
- **Accessibility-first:** Use semantic HTML and ARIA best practices.

## 📁 Project Structure and Styling

- **App Router:** Assume all new routes use the `app/` directory structure.
- **Styling:** Use [Tailwind CSS](tailwindcss.com) utility classes for styling. Only use CSS modules if absolutely necessary for complex, global styles.
- **Import Alias:** Use `@/*` for all imports from the `src/` directory.
- **Component Guidelines:**
  - Use functional components with hooks only.
  - Keep components small and focused.
  - Prefer `children: React.ReactNode` in props definitions.

## 🚀 Next.js Specifics

- **Images:** Use the `next/image` component for all images. Always include `alt`, `width`, `height`, and `sizes` props (or use `fill`).
- **Fonts:** Use `next/font` for automatic font optimization.
- **Navigation:** Use the `<Link>` component from `next/link` for all internal navigation, leveraging its default prefetching behavior.
- **Data Fetching:** Prefer server-side data fetching using `fetch` or Server Actions in Server Components.

## Example Usage

If I ask you to "Create a new page component for user settings", you should:

1.  Create a file at `src/app/settings/page.tsx` using a Server Component.
2.  Use Tailwind CSS for styling the form elements.
3.  Implement a mock "Save" button using a Server Action (e.g., `async function saveSettings(formData)`).
