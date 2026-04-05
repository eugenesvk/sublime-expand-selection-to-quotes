import sublime, sublime_plugin

class ExpandSelectionToQuotesCommand(sublime_plugin.TextCommand):
	q_same = ('"', "'", "`")
	esc = {'':'\\', # TODO: add more non\ escaping languages (custom symbol and quote repeats)
		'source.ahk':'`',
		'source.python':'\\',
	}
	esc_self = {'':('',), # languages that allow repeated quotes to escape themselves
		'source.ahk.1':('"',"'"),
	}

	def run(self, edit):
		# Official settings collate/cascade ≠ .update, but replace ≝top-level keys, so no granular updates → don't use .sublime-settings within the package
		cfg = sublime.load_settings('Expand Selection To Quotes.sublime-settings')
		self.q_same    = cfg.get('q_same'      	,self.q_same)
		self.esc     .update(cfg.get('esc'     	,{}))
		self.esc_self.update(cfg.get('esc_self'	,{}))

		q_all = {}
		for q in self.q_same:
			q_all[q] = list(map(lambda x: x.begin(), self.view.find_all(q)))

		def search_for_quotes(q_type, quotes, esc, esc_self):
			q_size, before, after = False, False, False

			if len(quotes) - self.view.substr(sel).count('"') >= 2:
				all_before = list(filter(lambda x: x <  sel.begin(), quotes))
				all_after  = list(filter(lambda x: x >= sel.end  (), quotes))
				before, after = None, None

				if all_before: # Find escaped quotes and skip them
					for  i_q in reversed(all_before):
						if i_q == 0:
							before = i_q
							break
						else:
							char_pre_q = self.view.substr(i_q - 1)
							if   char_pre_q == esc:
								pass
							elif char_pre_q == q and q in esc_self:
								pass
							else:
								before = i_q
								break
				if all_after:
					skip_paired = False
					for  i_q in          all_after  :
						if skip_paired:
							skip_paired = False
							continue

						if i_q == 0: # shouldn't happen, but just in case
							after = i_q
							break
						else:
							char_pre_q = self.view.substr(i_q - 1)
							char_pos_q = None if (i_q+1) >= self.view.__len__() else self.view.substr(i_q + 1)
							# print(f"{i_q} ? {self.view.__len__()} char_pos_q={char_pos_q}")
							if   char_pre_q == esc:
								pass
							elif char_pos_q == q and q in esc_self: # double quote as escape
								skip_paired = True
								pass
							else:
								after = i_q
								break

				if before is not None and after is not None: q_size = after - before

			return q_size, before, after

		def replace_region(start, end):
			if sel.size() < end-start-2:
				start += 1; end -= 1
			self.view.sel().subtract(sel)
			self.view.sel().add(sublime.Region(start, end))

		for sel in self.view.sel():
			ctx = self.view.scope_name(sel.a) #e.g., source.python meta.function…
			ctx_source = ctx.split()[0]       #      source.python
			esc      = self.esc     .get(ctx_source, self.esc     [''])
			esc_self = self.esc_self.get(ctx_source, self.esc_self[''])

			q_res = {}
			for q in self.q_same:
				sz, pre, pos = search_for_quotes(q,q_all[q], esc, esc_self)
				q_res[sz] = (pre,pos)

			min_sz = None
			for sz in q_res: # find the nearest quotes…
				if sz:
					if not min_sz:
						min_sz =     sz
					else:
						min_sz = min(sz, min_sz)
			if min_sz:      # …use their region for selection
				replace_region(q_res[min_sz][0], q_res[min_sz][1] + 1)
