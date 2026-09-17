# Node.js Framework Profile

The **Node.js Framework Profile** supports JavaScript and TypeScript server-side and fullstack applications.

---

## Commands

- **Analyze / Lint**: `npm run lint`
- **Format**: `npm run format`
- **Unit Tests**: `npm test` or `node --test`
- **Integration / E2E**: `npm run test:e2e` (conditional on test scripts in `package.json`)
- **Build**: `npm run build`

---

## Conventions
- State/Architecture: Express, NestJS, Fastify, Modular monolith.
- Module format: ES Modules (`import/export`) or CommonJS (`require`).
