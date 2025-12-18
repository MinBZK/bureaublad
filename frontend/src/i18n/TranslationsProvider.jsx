"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { createTranslator, getTranslations } from "./config";
import { useLanguage } from "./LanguageContext";

const TranslationsContext = createContext({});

export function TranslationsProvider({ children, initialMessages }) {
  const { locale } = useLanguage();
  const [messages, setMessages] = useState(initialMessages);
  useEffect(() => {
    async function loadMessages() {
      const newMessages = await getTranslations(locale);
      setMessages(newMessages);
    }
    loadMessages();
  }, [locale]);

  return (
    <TranslationsContext.Provider value={messages}>
      {children}
    </TranslationsContext.Provider>
  );
}

export function useTranslations(namespace) {
  const messages = useContext(TranslationsContext);
  return createTranslator(messages, namespace);
}
