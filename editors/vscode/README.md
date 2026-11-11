# SlowLang - VS Code extension

Syntax highlighting for `.slow` files. SlowLang executes as Python, so the
grammar is the built-in Python grammar plus the `please()` keyword
(scoped `keyword.other.slowlang`).

## Publish (one-time, needs a publisher account)

1. Create a publisher at https://marketplace.visualstudio.com/manage
   (sign in with a Microsoft account, create an Azure DevOps org when asked,
   publisher ID `sebin-gg` to match package.json).
2. `npm i -g @vscode/vsce` then `vsce login sebin-gg` (paste a DevOps PAT
   with Marketplace > Manage scope).
3. From this directory: `vsce package` then `vsce publish`.
4. Mirror to Open VSX: `npx ovsx publish -p <token>` (signup at
   https://open-vsx.org via Eclipse account).

SlowLang won TinkerHub Useless Projects 2.0. Demo: https://sebin-gg.github.io/slowlang/
