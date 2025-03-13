export default function SiteAlert() {
  return (
    <div className="rvo-alert rvo-alert--info rvo-alert--padding-md" data-alert-id="index-poc-alert">
            <span className="utrecht-icon rvo-icon rvo-icon-info rvo-icon--xl rvo-status-icon-info" role="img"
                  aria-label="Info"></span>
      <div className="rvo-alert-text">
        <strong>Proof of Concept</strong>
        <div>
          <div>
            Dit systeem is nog in ontwikkeling. Er zijn geen garanties dat
            de data veilig blijft of bewaard blijft.
          </div>
        </div>
      </div>
      <button className="utrecht-button utrecht-button--subtle rvo-button__close utrecht-button--rvo-md"
              type="button" aria-label="Sluiten">
              <span className="utrecht-icon rvo-icon rvo-icon-kruis rvo-icon--md rvo-icon--hemelblauw" role="img"
                    aria-label="Kruis"></span>
      </button>
    </div>
  )
}
