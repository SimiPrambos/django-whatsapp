const Menu = [
  { header: 'Apps' },
  {
    title: 'Dashboard',
    group: 'apps',
    icon: 'dashboard',
    name: 'Dashboard',
    href: '/dashboard'
  },
  {
    title: 'Numbers',
    group: 'apps',
    icon: 'mdi-whatsapp',
    name: 'Numbers',
    href: '/numbers'
  },
  {
    title: 'Contacts',
    group: 'apps',
    icon: 'contacts',
    name: 'Contacts',
    href: '/contacts'
  },
  {
    title: 'Media',
    group: 'apps',
    icon: 'perm_media',
    name: 'Media',
    href: '/mediafile'
  },
  { header: 'Messages' },
  {
    title: 'Create',
    group: 'messages',
    icon: 'mdi-send',
    name: 'Create',
    href: '/messages/create'
  },
  {
    title: 'Inbox',
    group: 'messages',
    icon: 'mdi-inbox-arrow-down',
    name: 'Inbox',
    href: '/messages/inbox'
  },
  {
    title: 'Outbox',
    group: 'messages',
    icon: 'mdi-inbox-arrow-up',
    name: 'Outbox',
    href: '/messages/outbox'
  },
  { header: 'Settings' },
  {
    title: 'Webhook',
    group: 'settings',
    icon: 'mdi-webhook',
    name: 'Webhook',
    href: '/settings/webhook'
  }
];
// reorder menu
Menu.forEach((item) => {
  if (item.items) {
    item.items.sort((x, y) => {
      let textA = x.title.toUpperCase();
      let textB = y.title.toUpperCase();
      return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
    });
  }
});

export default Menu;
