import {
  AppstoreOutlined,
  AudioOutlined,
  CalendarOutlined,
  CheckSquareOutlined,
  CloudOutlined,
  CommentOutlined,
  FileTextOutlined,
  FolderOpenOutlined,
  MailOutlined,
  MessageOutlined,
  ProjectOutlined,
  TableOutlined,
  VideoCameraOutlined,
} from "@ant-design/icons";

const APP_ICONS = {
  calendar: CalendarOutlined,
  conversation: MessageOutlined,
  docs: FileTextOutlined,
  dictaphone: AudioOutlined,
  drive: CloudOutlined,
  email: MailOutlined,
  grist: TableOutlined,
  matrix: CommentOutlined,
  meet: VideoCameraOutlined,
  ocs: FolderOpenOutlined,
  projects: ProjectOutlined,
  task: CheckSquareOutlined,
};

export const appIcon = (app) => APP_ICONS[app?.id] || AppstoreOutlined;
