const dict: Record<string, Record<string, string>> = {
  pt: { modules: "Módulos", back: "Voltar" },
  en: { modules: "Modules", back: "Back" },
};

export function t(lang: string, key: string) {
  return dict[lang]?.[key] || key;
}
