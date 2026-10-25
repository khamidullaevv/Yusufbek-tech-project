import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        midnight: "#08111f",
        panel: "#101c2d",
        mint: "#51e0b3",
      },
    },
  },
  plugins: [],
};

export default config;
