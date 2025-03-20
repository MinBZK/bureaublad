function iconInfoByFilename(filename: string): {iconName: string, iconTitle: string} {
  const indexOfExtensionDot = filename.lastIndexOf(".");
  const extension = indexOfExtensionDot > -1 ? filename.substring(indexOfExtensionDot + 1) : '';
  if (extension) {
    switch(extension) {
      case 'odt':
      case 'doc':
      case 'docx':
      case 'txt':
      case 'rtf':
      case 'pdf':
      {
        return {
          iconName: 'rvo-icon-document-met-vlakken-en-lijnen-erop',
          iconTitle: 'Document met vlakken en lijnen erop'
        }
      }
      case 'xls':
      case 'xlsx':
      case 'ods':
      {
        return {
          iconName: 'rvo-icon-grafiek',
          iconTitle: 'Grafiek'
        }
      }
      case 'ppt':
      case 'pptx':
      case 'odp':
      {
        return {
          iconName: 'rvo-icon-bord-met-grafieken',
          iconTitle: 'Bord met grafieken'
        }
      }
      default: {
        return {
          iconName: 'rvo-icon-document-blanco',
          iconTitle: 'Document blanco'
        }
      }
    }
  }
  return {
    iconName: 'rvo-icon-map',
    iconTitle: 'Map'
  }
}

export default function FileTypeIcon({ fileName }){
  const iconInfo = iconInfoByFilename(fileName);
  return (
    <span className={'utrecht-icon rvo-icon ' + iconInfo.iconName + ' rvo-icon--xl rvo-icon--hemelblauw'} role="img"
          aria-label={iconInfo.iconTitle}></span>
  )
}