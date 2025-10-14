"use client";
import React, { RefObject, useEffect, useRef } from "react";
import { createPortal } from "react-dom";

interface CustomModalProps {
  onClose: () => void;
  children: React.ReactNode;
  title: string;
}

export function CustomModal({ onClose, children, title }: CustomModalProps) {
  const popoverRef: RefObject<HTMLDivElement | null> = useRef(null);
  const closeRef: RefObject<HTMLAnchorElement | null> = useRef(null);

  useEffect(() => {
    function handler(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }

    document.addEventListener("keydown", handler);
    return () => {
      document.removeEventListener("keydown", handler);
    };
  }, [onClose]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        (popoverRef.current &&
          !popoverRef.current.contains(event.target as Node)) ||
        (closeRef.current && closeRef.current.contains(event.target as Node))
      ) {
        onClose();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [onClose]);

  const containerRoot = document.querySelector("#modal-container");

  return containerRoot
    ? createPortal(
        <div className="modal-overlay">
          <div className="modal-wrapper">
            <div className="modal" ref={popoverRef}>
              <div className="modal-header">
                <span
                  className="utrecht-icon rvo-icon rvo-icon-kruis rvo-icon--md rvo-icon--hemelblauw rvo-dialog__close-icon"
                  role="img"
                  aria-label="Kruis"
                  ref={closeRef}
                ></span>
              </div>
              <div className="modal-body rvo-scrollable-content">
                {title && <h2>{title}</h2>}
                {children}
              </div>
            </div>
          </div>
        </div>,
        containerRoot,
      )
    : null;
}
