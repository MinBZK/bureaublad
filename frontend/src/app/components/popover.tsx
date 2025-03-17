import React, { useState, useRef, useEffect } from 'react';
import './popover.css';

const Popover = ({ children, content, onClickHandler, buttonClassName }) => {
  const [isVisible, setIsVisible] = useState(false); // Manages the visibility state of the popover
  const popoverRef = useRef(null); // Reference to the popover element
  const triggerRef = useRef(null); // Reference to the button element that triggers the popover

  const handleOnClick = () => {
    setIsVisible(true);
    onClickHandler();
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        popoverRef.current &&
        !popoverRef.current.contains(event.target) &&
        !triggerRef.current.contains(event.target)
      ) {
        setIsVisible(false); // Close the popover if clicked outside
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  {/*  >*/}
  {/*  <Popover.Description className="rvo-card__content">*/}
  return (
    <div className="popover-container">
      <button
        ref={triggerRef}
        onClick={handleOnClick}
        className={buttonClassName + ' popover-trigger'}
        aria-haspopup="true"
        aria-expanded={isVisible}
        aria-controls="popover-content"
      >
        {children}
      </button>
      {isVisible && (
        <div
          id="popover-content"
          ref={popoverRef}
          className="rvo-card rvo-card--outline rvo-card--padding-sm openbsw-search-card popover-content"
          role="dialog"
          aria-modal="true"
        >
          {content}
        </div>
      )}
    </div>
  );
};

export default Popover;